
import random

from django.db import models
from django.db.models import F

from django.conf import settings


class Galaxy(models.Model):
    galaxy = models.IntegerField(default=0, unique=True)
    X_RADIUS = models.IntegerField(default=20)
    Y_RADIUS = models.IntegerField(default=20)


def _random_choice(choices):
    """
    Choose one from the django models choices option, returning its
    database portion.
    """
    return random.choice(choices)[0]


PLANET_SIZES = (
    (0, 'miniscule'),
    (1, 'tiny'),
    (2, 'small'),
    (3, 'medium'),
    (4, 'large'),
    (5, 'great'),
    (6, 'gigantic'),
)

PLANET_ORBITS = (
    (0, 'unbearably hot and spinning close the its sun'),
    (1, 'warm due to its proximity to the sun'),
    (2, 'with a pleasant warthm from the sun'),
    (3, 'of a temperate climate'),
    (4, 'somewhat cooled by the distance to its sun'),
    (5, 'rather colder than preferred'),
    (6, 'far from its sun'),
)

PLANET_DESC = '''
A {size}, {greenness} planet, {orbit}, with {minerals} minerals hidden below the surface.
'''

class Planet(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()
    size = models.IntegerField(choices=PLANET_SIZES)
    orbit = models.IntegerField(choices=PLANET_ORBITS)

    greenness = models.IntegerField() # 0 - 100
    minerals = models.IntegerField() # 0 - 100

    #TODO Departed time, charred desc

    class Meta:
        unique_together = (
            ('x', 'y'),
        )

    @classmethod
    def create_planet(cls, x, y):
        size = _random_choice(PLANET_SIZES)
        orbit = _random_choice(PLANET_ORBITS)
        greenness = random.randint(0, 100)
        minerals = random.randint(45, 100 - greenness)
        planet = cls(x=x, y=y, size=size, greenness=greenness, minerals=minerals)
        return planet

    def get_greenness_desc(self):
        if self.greenness >= 80:
            return 'thickly overgrown'
        elif self.greenness >= 60:
            return 'lush'
        elif self.greenness >= 40:
            return 'green'
        elif self.greenness >= 20:
            return 'desert'
        else:
            return 'barren'

    def get_mineral_desc(self):
        if self.minerals >= 80:
            return 'abundant'
        elif self.minerals >= 60:
            return 'many'
        elif self.minerals >= 40:
            return 'deposits of'
        elif self.minerals >= 20:
            return 'a small concentration'
        else:
            return 'traces of'

    def description(self):
        return PLANET_DESC.format(
                size=self.get_size_display(),
                greenness=self.get_greenness_desc(),
                orbit=self.get_orbit_display(),
                minerals=self.get_mineral_desc()
                )

def get_location(x, y):
    try:
        return Planet.objects.get(x=x, y=y)
    except Planet.DoesNotExist:
        return None


def get_dir(dx, dy):
    N_S = {1:'N', 0:'', -1:'S'}
    E_W = {1:'E', 0:'', -1:'W'}
    return N_S[dy] + E_W[dx]


def get_lrs(ship):
    galaxy = Galaxy.objects.get(galaxy=0)
    x_s = (-1, 0, 1)
    y_s = (-1, 0, 1)
    if ship.x == galaxy.X_RADIUS:
        x_s = x_s[:2]
    elif ship.x == -galaxy.X_RADIUS:
        x_s = x_s[1:]
    if ship.y == galaxy.Y_RADIUS:
        y_s = y_s[:2]
    elif ship.y == -galaxy.Y_RADIUS:
        y_s = y_s[1:]
    coords = [
            [(x, y) for x in x_s]
                for y in y_s]
    planets = [
            [(get_dir(*loc), loc[0], loc[1], get_location(ship.x + loc[0], ship.y + loc[1])) for loc in row]
                for row in coords]
    planets.reverse()
    return planets


EVENTS = (
    (0, 'Nothing'),
    (1, 'Alien Ruins Discovered'),
    (2, 'Pirate Attack'),
    (3, 'Hostile Aliens'),
    (4, 'Dangerous Nebula'),
    (5, 'Killer Virus'),
)


class Ship(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    tutorial_step = models.IntegerField(default=0)

    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)

    population = models.IntegerField(default=1)
    living_space = models.IntegerField(default=10)

    restlessness = models.IntegerField(default=0) # 0-
    happiness = models.IntegerField(default=50) # 0-100

    farms = models.IntegerField(default=1)
    food = models.IntegerField(default=5)
    freezer_space = models.IntegerField(default=10)

    miners = models.IntegerField(default=1)
    metal = models.IntegerField(default=5)
    cargo_space = models.IntegerField(default=10)

    research = models.IntegerField(default=0)
    structure_tech = models.IntegerField(default=8)
    maintainence_tech = models.IntegerField(default=0)
    contentment_tech = models.IntegerField(default=0)

    current_event = models.IntegerField(choices=EVENTS, default=0)

    has_sub_surface_scanner = models.BooleanField(default=False)
    has_defense_system = models.BooleanField(default=False)
    has_alien_translator = models.BooleanField(default=False)
    has_particle_shield = models.BooleanField(default=False)
    has_omni_anti_virus = models.BooleanField(default=False)

    def structure(self):
        return (
                (self.living_space + self.freezer_space + self.cargo_space) // 10
                + self.farms + self.miners
        )


    STRUCTURE = {
        'living_space',
        'freezer_space',
        'cargo_space',
        'farm',
        'miner',
    }

    COST_BUILD = dict(
        living_space=10,
        freezer_space=10,
        cargo_space=10,
        farm=10,
        miner=10,
        sub_surface=10,
        defences=10,
        translator=10,
        shield=10,
        anti_virus=10,
    )

    COST_RESEARCH = dict(
        structure=10,
        maintainence=10,
        contentment=10,
    )


    def get_orbitting(self):
        return get_location(self.x, self.y)

    def get_productivity(self):
        return 1 + (self.happiness - 50) / 100


# Effects are a tuple:
# (Description, Resource modified, Good or Bad, Change)

def _get_base_effects(ship):
    effects = []

    eaten = min(ship.population, ship.food)
    effects.append(('Food Eaten', 'food', '-', -eaten))
    starvation = ship.population - eaten
    if starvation > 0:
        effects.append(('Starvation', 'happiness', '-', -starvation * 10))
        # Can't run out of population:
        if starvation == ship.population:
            starvation -= 1
        if starvation:
            effects.append(('Starvation', 'population', '-', -int(starvation / 2) - 1))
    elif ship.food > 5:
        if ship.population < ship.living_space:
            effects.append(('Population Growth', 'population', '+', 1))
            effects.append(('Population Growth', 'happiness', '+', 10))
            effects.append(('Population Growth', 'food', '-', -5))
        else:
            effects.append(('Overcrowding', 'happiness', '-', -10))

    farm_max = min(ship.population, ship.farms)
    effects.append(('Farm Surplus', 'food', '+', int(farm_max * ship.get_productivity() + 0.5)))

    if ship.restlessness:
        effects.append(('Restlessness', 'happiness', '-', -ship.restlessness))

    effects.append(('Research', 'research', '+', ship.population))

    return effects


def get_effects_stay(ship, planet):
    effects = _get_base_effects(ship)

    effects.append(('Planetary Farming', 'food', '+', ship.population * (planet.greenness + 25) // 25))

    miner_max = min(ship.population, ship.miners)
    effects.append(('Planetary Mining', 'metal', '+', int(miner_max * ship.get_productivity() * (planet.minerals + 25) // 25 + 1)))

    effects.append(('Solid Ground Underfoot', 'happiness', '+', 10))
    effects.append(('Restlessness', 'restlessness', '-', 2))

    return effects


def get_effects_travel(ship):
    effects = _get_base_effects(ship)

    farm_maint = 2 * ship.farms - min(ship.farms, ship.maintainence_tech)
    farm_decay = farm_maint - ship.metal
    effects.append(('Farm Maintenance', 'metal', '-', -farm_maint))
    # Always keep the last farm:
    if farm_decay - ship.farms == 0:
        farm_decay -= 0
    if farm_decay > 0:
        effects.append(('Farm Exhaustion', 'farms', '-', -int(farm_decay/2) - 1))

    if ship.restlessness:
        effects.append(('Traveling', 'restlessness', '+', -1))

    return effects


def apply_effects(ship, effects):
    for effect in effects:
        _desc, stat, _good, diff = effect
        setattr(ship, stat, diff + getattr(ship, stat))

    ship.population = max(1, min(ship.population, ship.living_space))
    ship.food = max(0, min(ship.food, ship.freezer_space))
    ship.metal = max(0, min(ship.metal, ship.cargo_space))
    ship.happiness = max(0, min(ship.happiness, 100))
    ship.restlessness = max(0, min(ship.restlessness, 100))


def leave_planet(planet):
    planet.greenness =  3 * F('greenness') / 4
    planet.save()


def mine_planet(planet, miners):
    planet.minerals = F('minerals') - min(miners // 2, 1)
    planet.save()

