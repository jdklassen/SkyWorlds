
import random

from django.db import models

from django.conf import settings


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
A {size}, {greeness} planet, {orbit}, with {minerals} minerals hidden below the ground.
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
                greeness=self.get_greenness_desc(),
                orbit=self.get_orbit_display(),
                minerals=self.get_mineral_desc()
                )

def get_location(x, y):
    try:
        return Planet.objects.get(x=x, y=y)
    except Planet.DoesNotExist:
        return None


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
    maintainence_tech = models.IntegerField(default=1)
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
        structure=100,
        maintainence=100,
        contentment=100,
    )


    def get_orbitting(self):
        return get_location(self.x, self.y)

    def get_neighbourhood(self):
        x = self.x
        y = self.y
        return [
            [get_location(x-1,y+1), get_location(x,y+1), get_location(x+1,y+1)],
            [get_location(x-1,y  ), get_location(x,y  ), get_location(x+1,y  )],
            [get_location(x-1,y-1), get_location(x,y-1), get_location(x+1,y-1)],
        ]

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
        else:
            effects.append(('Overcrowding', 'happiness', '-', -10))

    farm_max = min(ship.population, ship.farms)
    effects.append(('Farm Surplus', 'food', '+', int(farm_max * ship.get_productivity() + 1)))

    if ship.restlessness:
        effects.append(('Restlessness', 'happiness', '-', -ship.restlessness))

    return effects


def get_effects_stay(ship, planet):
    effects = _get_base_effects(ship)

    effects.append(('Planetary Farming', 'food', '+', ship.population * (planet.greenness + 25) // 25))

    miner_max = min(ship.population, ship.miners)
    effects.append(('Planetary Mining', 'metal', '+', int(miner_max * ship.get_productivity() * (planet.minerals + 25) // 25 + 1)))

    effects.append(('Solid Ground Underfoot', 'happiness', '+', 10))
    effects.append(('Restlessness', 'restlessness', '-', 4))

    return effects


def get_effects_travel(ship):
    effects = _get_base_effects(ship)

    farm_maint = 2 * ship.farms - min(ship.farms, ship.maintainence_tech)
    farm_decay = ship.metal - farm_maint
    effects.append(('Farm Maintenance', 'metal', '-', -farm_maint))
    # Always keep the last farm:
    if farm_decay - ship.farms == 0:
        farm_decay -= 0
    if farm_decay > 0:
        effects.append(('Farm Exhaustion', 'farms', '-', -int(farm_decay/2) - 1))

    if ship.restlessness:
        effects.append(('Traveling', 'restlessness', '+', -1))

    return effects

