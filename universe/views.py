
import random

from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponseBadRequest
from django.db.models import Avg, StdDev, Count

from .models import Galaxy, Planet, Ship
from .models import get_effects_travel, get_effects_stay, get_lrs
from .models import apply_effects, mine_planet, leave_planet
from .models import get_location


INDEX_TEMPLATE = 'universe/index.html'
CONTROL_PANEL = 'universe/control.html'


@login_required
def index(request):
    ship = request.user.ship
    planet = ship.get_orbitting()
    context = dict(
            ship=ship,
            planet=planet,
            travel=get_effects_travel(ship),
            lrs=get_lrs(ship),
            )
    if planet:
        context['stay'] = get_effects_stay(ship, planet)
    return render(request, INDEX_TEMPLATE, context)


@login_required
def build(request, item_name):
    ship = request.user.ship
    cost = ship.COST_BUILD.get(item_name, 0)
    if item_name not in ship.COST_BUILD:
        # Don't know what this thing is; redirect.
        return redirect('index')
    elif ship.metal < cost:
        # Can't afford it; redirect.
        return redirect('index')
    elif item_name in ship.STRUCTURE and ship.structure() == ship.structure_tech:
        # Won't fit in ship; redirect.
        return redirect('index')

    ship.metal -= cost
    if item_name == 'living_space':
        ship.living_space += 10
    elif item_name == 'freezer_space':
        ship.freezer_space += 10
    elif item_name == 'cargo_space':
        ship.cargo_space += 10
    elif item_name == 'farm':
        ship.farms += 1
    elif item_name == 'miner':
        ship.miners += 1
    elif item_name == 'sub_surface':
        ship.has_sub_surface_scanner = True
    elif item_name == 'defences':
        ship.has_defense_system = True
    elif item_name == 'translator':
        ship.has_alien_translator = True
    elif item_name == 'shield':
        ship.has_particle_shield = True
    elif item_name == 'anti_virus':
        ship.has_omni_anti_virus = True
    ship.save()
    return redirect('index')


@login_required
def research(request, tech_name):
    ship = request.user.ship
    cost = ship.research_cost(tech_name)
    if tech_name not in ship.COST_RESEARCH:
        return redirect('index')

    ship.research -= cost
    if tech_name == 'structure':
        ship.structure_tech += 1
    elif tech_name == 'maintainence':
        ship.maintainence_tech += 1
    elif tech_name == 'contentment':
        ship.contentment_tech += 1
    ship.save()
    return redirect('index')


@login_required
def stay(request):
    ship = request.user.ship
    planet = ship.get_orbitting()
    if not planet:
        return redirect('index')

    # Apply effects:
    effects = get_effects_stay(ship, planet)
    apply_effects(ship, effects)

    # Affect planet:
    mine_planet(planet, ship.miners)

    ship.check_for_event()

    ship.save()
    return redirect('index')


@login_required
def travel(request, dx, dy):
    try:
        dx = int(dx)
        dy = int(dy)
    except Exception:
        return redirect('index')
    if dx not in (-1, 0, 1) or dy not in (-1, 0, 1):
        return redirect('index')
    ship = request.user.ship

    # Apply effects:
    effects = get_effects_travel(ship)
    apply_effects(ship, effects)

    # Affect planet:
    planet = ship.get_orbitting()
    if planet:
        leave_planet(planet)

    # Move ship:
    ship.x += dx
    ship.y += dy

    ship.check_for_event()

    ship.save()
    return redirect('index')


@login_required
def populate(request, x=20, y=20, p=5, forced=False):
    x = int(x)
    y = int(y)
    p = int(p)
    if request.user.is_staff:
        try:
            galaxy = Galaxy.objects.get(galaxy=0)
            if not forced and (x < galaxy.X_RADIUS or y < galaxy.Y_RADIUS):
                # Can't shrink the world without a reset!
                return HttpResponseBadRequest('Must use Force to shink the Galaxy!')
            xs = list(range(-x,-galaxy.X_RADIUS)) + list(range(galaxy.X_RADIUS + 1, x + 1))
            ys = list(range(-y,-galaxy.Y_RADIUS)) + list(range(galaxy.Y_RADIUS + 1, y + 1))
            galaxy.X_RADIUS = x
            galaxy.Y_RADIUS = y
        except Galaxy.DoesNotExist:
            galaxy = Galaxy(galaxy=0, X_RADIUS=x, Y_RADIUS=y)
            xs = range(-x-1, x+2)
            ys = range(-y-1, y+2)
        galaxy.save()
        if forced:
            xs = range(-x-1, x+2)
            ys = range(-y-1, y+2)
            Planet.objects.all().delete()
        for x in xs:
            for y in ys:
                if random.randint(1,p) == 1:
                    planet = Planet.create_planet(x=x, y=y)
                    planet.save()
        return redirect('controls')
    return redirect('index')


@login_required
def controls(request):
    if request.user.is_staff:
        g = Galaxy.objects.get(galaxy=0)
        llrs = [
                [get_location(x, y) for x in range(-g.X_RADIUS, g.X_RADIUS+1)]
                    for y in reversed(range(-g.Y_RADIUS, g.Y_RADIUS+1))]
        if settings.DATABASES['default']['ENGINE'].endswith('sqlite3'):
            StdDev2 = lambda s: Count(s)
        else:
            StdDev2 = StdDev
        planets = Planet.objects.all().aggregate(
                ave_green=Avg('greenness'),
                std_green=StdDev2('greenness'),
                ave_minerals=Avg('minerals'),
                std_minerals=StdDev2('minerals'),
                )
        context = dict(
            ships=Ship.objects.count(),
            llrs=llrs,
            planets=planets,
            )
        return render(request, CONTROL_PANEL, context)
    return redirect('index')

