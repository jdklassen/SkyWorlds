
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .models import Planet, Ship
from .models import get_effects_travel, get_effects_stay, get_lrs
from .models import apply_effects, mine_planet, leave_planet


INDEX_TEMPLATE = 'universe/index.html'


@login_required
def index(request):
    ship = request.user.ship
    planet = ship.get_orbitting()
    #TODO stay/travel buttons
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
    base_cost = ship.COST_RESEARCH.get(tech_name, 0)
    if tech_name not in ship.COST_RESEARCH:
        return redirect('index')
    elif tech_name == 'structure':
        cost = base_cost * (ship.structure_tech + -7)
        if cost > ship.research:
            return redirect('index')
        ship.research -= cost
        ship.structure_tech += 1
    elif tech_name == 'maintainence':
        cost = base_cost * (ship.maintainence_tech + 1)
        if cost > ship.research:
            return redirect('index')
        ship.research -= cost
        ship.maintainence_tech += 1
    elif tech_name == 'contentment':
        cost = base_cost * (ship.contentment_tech + 1)
        if cost > ship.research:
            return redirect('index')
        ship.research -= cost
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

    #TODO possible events

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

    #TODO possible events

    # Move ship:
    ship.x += dx
    ship.y += dy
    ship.save()
    return redirect('index')

