import pygame, os
import os
import json
from copy import deepcopy
from functools import partial
import data.components
from data.components import *
from engine.ecs.exceptions import NonexistentComponentTypeForEntity

class Maker(object):

    __slots__ = 'em', 'game' 
    presets = {}

    def __init__(self, entity_manager, entity_path=None, game=None):

        self.em = entity_manager
        self.game = game

        if entity_path:
            self.update_presets(entity_path)

    def update_presets(self, entity_path):
        # iterate over entities in the directory
        for preset in os.listdir(entity_path):
            # open the json file representing the entity
            with open(os.path.join(entity_path, preset)) as pref:
                try:
                    cp_pre = json.load(pref)
                except ValueError:
                    print('Failed to read in preset', preset)
                    continue

            # read the name of the entity
            try:
                name = cp_pre['Misc']['name']
            except KeyError:
                print('No name for preset', preset)
                continue


            vargs = [] # I think this stores
            compargs = {'vargs': vargs} # component arguments
            self.presets[name] = compargs # save this entity in presets

            # iterate fields in the entity file
            for s in cp_pre:
                if s == 'Misc': continue # misc processed about to get the name

                try:
                    # . means it's in the form component.factory
                    if '.' in s:
                        c, fac, *_ = s.split('.')
                        comp = getattr(getattr(data.components, c), fac)
                    else:
                        comp = getattr(data.components, s)
                    # comp is now the method that will create the entity
                except AttributeError as err:
                    print(s)
                    print('Component or Factory doesnt exist')
                    del self.presets[name]
                    break

                # map this component to it's default arguments
                compargs[comp] = {}

                # iterate fields for this component
                for key, val in cp_pre[s].items():
                    # if it's not a string or it doesn't start with $ 
                    # (such as 'size': '$1'...), store it in the component arguments
                    if not isinstance(val, str) or val[0] != '$':
                        compargs[comp][key] = val
                        continue

                    # strip leading $ and convert to int
                    try:
                        n = int(val[1:])
                    except ValueError:
                        print('couldnt read the preset', val[1:])
                        del self.presets[name]
                        break


                    while n >= len(vargs):
                        vargs.append ([])

                    vargs[n].append((comp, key))
                else:
                    continue

                break

    def make(self, name, *vargs, pos=(0, 0)):

        try:
            proto = self.presets[name].copy()
        except KeyError:
            raise ValueError ('Preset {} doesn\'t exist.'.format(name)) from None

        for i, va in enumerate(proto['vargs']):
            try:
                for c, o in va:
                    proto[c][o] = vargs[i]
            except IndexError:
                print('Preset "{}" specified more arguments than were provided.'.format(name))
                return
        del proto['vargs']

        e = self.em.create_entity()
        if pos:
            self.em.add_component(e, Position(*pos))

        for c, args in proto.items():
            self.em.add_component(e, c(**args))
        return e

    def __getitem__(self, name):
        return partial (self.make, name)

