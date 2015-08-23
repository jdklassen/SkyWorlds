
import random
from datetime import datetime, timedelta

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
    (0, 'unbearably hot and spinning close its sun'),
    (1, 'warm due to its proximity to the sun'),
    (2, 'with a pleasant warthm from the sun'),
    (3, 'of a temperate climate'),
    (4, 'somewhat cooled by the distance to its sun'),
    (5, 'rather colder than preferred'),
    (6, 'far from its sun'),
)

PLANET_DESC = '''
a {size}, {greenness} planet, {orbit}, with {minerals} minerals hidden below the surface.
'''

class Planet(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()
    size = models.IntegerField(choices=PLANET_SIZES)
    orbit = models.IntegerField(choices=PLANET_ORBITS)
    last_charred = models.DateTimeField(null=True)

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
        desc = PLANET_DESC.format(
                size=self.get_size_display(),
                greenness=self.get_greenness_desc(),
                orbit=self.get_orbit_display(),
                minerals=self.get_mineral_desc()
                )
        if self.last_charred is not None and datetime.now() - self.last_charred < timedelta(minutes=5):
            desc += ' A Large portion of the surface looks charred, as if there was a great fire recently.'
        return desc

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
    name = models.CharField(max_length=100)
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
    BASE_TECH = dict(
        structure=-7,
        maintainence=1,
        contentment=1,
    )
    def research_cost(self, tech):
        base_cost = self.COST_RESEARCH.get(tech, 0)
        base_tech = self.BASE_TECH.get(tech, 0)
        current_tech = getattr(self, tech + '_tech', 0)
        cost = base_cost * (current_tech + base_tech)
        return cost


    def get_orbitting(self):
        return get_location(self.x, self.y)

    def get_productivity(self):
        return 1 + (self.happiness - 50) / 100

    def check_for_event(self):
        self.current_event = 0
        if self.get_orbitting():
            ruins = random.random()
            if self.has_sub_surface_scanner and ruins > .95:
                self.current_event = 1
            elif ruins > .99:
                self.current_event = 1
            elif random.random() > .99:
                self.current_event = 3
            elif random.random() > .99:
                self.current_event = 5
        else:
            if random.random() > .99:
                self.current_event = 2
            elif random.random() > .99:
                self.current_event = 4

    def get_event_desc(ship):
        if ship.current_event == 1:
            return 'We unearthed some valuble materials in an ancient alien ruin.  I wonder who they were.'
        if ship.current_event == 2:
            if ship.has_defense_system:
                return 'We beat off some pirates and made a hansome salvage haul.'
            else:
                return 'We beat off the pirates in a drawn-out and costly fight.'
        if ship.current_event == 3:
            if ship.has_alien_translator:
                return 'We discovered some primitive aliens, and made some profitable trades.'
            else:
                return 'We discovered some primitive, but truculent aliens.  We have begun constant watches...'
        if ship.current_event == 4:
            if ship.has_particle_shield:
                return 'Some measurements we were able to make in this nebula might require some profound to some of our theories of matter.'
            else:
                return 'The particles from that nebula wreaked havoc on our farms.'
        if ship.current_event == 5:
            if ship.has_omni_anti_virus:
                return 'Our medical scientists have staved off a potentially catastrophic virus infection.'
            else:
                return 'A novel virus pandemic has cost us many lives...'
        return 'Nothing of interest happened...'


# Effects are a tuple:
# (Description, Resource modified, Good or Bad, Change)

def _get_effects_event(ship):
    effects = []

    if ship.current_event == 1:
        effects.append(('Alien Ruins', 'metal', '+', 5))
    if ship.current_event == 2:
        if ship.has_defense_system:
            effects.append(('Pirate Salvage', 'metal', '+', 5))
        else:
            effects.append(('Pirate Looting', 'metal', '-', -2))
            effects.append(('Pirate Looting', 'food', '-', -2))
    if ship.current_event == 3:
        if ship.has_alien_translator:
            effects.append(('Friendly Aliens', 'metal', '+', 2))
        else:
            effects.append(('Hostile Aliens', 'population', '-', -2))
    if ship.current_event == 4:
        if ship.has_particle_shield:
            effects.append(('Nebula Measurements', 'research', '+', 10))
        else:
            effects.append(('Nebula Damage Repair', 'metal', '-', -10))
            if ship.farms > 1:
                effects.append(('Nebula Damage', 'farms', '-', -1))
    if ship.current_event == 5:
        if ship.has_omni_anti_virus:
            effects.append(('Anti-Virus Research', 'research', '-', 10))
        else:
            effects.append(('Novel Virus Strain', 'population', '-', -3))

    return effects


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

    effects.extend(_get_effects_event(ship))

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

    farm_maint = ship.farms - min(2 * ship.farms // 3, ship.maintainence_tech)
    farm_decay = farm_maint - ship.metal
    if farm_maint:
        effects.append(('Farm Maintenance', 'metal', '-', -farm_maint))
    # Always keep the last farm:
    if farm_decay - ship.farms == 0:
        farm_decay -= 1
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
    ship.farms = max(1, ship.farms)
    ship.miners = max(1, ship.miners)
    ship.research = max(0, ship.research)
    ship.happiness = max(0, min(ship.happiness, 100))
    ship.restlessness = max(0, min(ship.restlessness, 100))


def leave_planet(planet):
    planet.greenness =  3 * F('greenness') / 4
    planet.last_charred = datetime.now()
    planet.save()


def mine_planet(planet, miners):
    planet.minerals = F('minerals') - min(miners // 2, 1)
    planet.save()

