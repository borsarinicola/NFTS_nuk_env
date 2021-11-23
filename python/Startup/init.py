# Add rez tokens to hiero shot export

from hiero.exporters.FnShotProcessor import ShotProcessorPreset
import hiero.core

def shot_addUserResolveEntries(self, resolver):
    
    def plateWidth(task):
        trackItem = task._item
        media = trackItem.source().mediaSource()
        return str(media.width())

    def plateHeight(task):
        trackItem = task._item
        media = trackItem.source().mediaSource()
        return str(media.height())
    
    def plateRez(task):
        rez = '{}x{}'.format(plateWidth(task), plateHeight(task))
        return rez

    def generate_project_code(task, project_name):
        temp_string = ''
        if len(project_name) <= 3:
            return project_name

        for aChar in project_name:
            if not aChar in ['a', 'e', 'i', 'o', 'u']:
                temp_string += aChar
        
            if len(temp_string) == 3:
                return temp_string
        


    resolver.addResolver("{width}", "Returns the width of the source plate", lambda keyword, task: plateWidth(task))
    resolver.addResolver("{height}", "Returns the height of the source plate", lambda keyword, task: plateHeight(task))
    resolver.addResolver("{rez}", "Returns the height Resoluton of the source palte (width x height)", lambda keyword, task: plateRez(task))
    resolver.addResolver("{project_code}", "Three letter project code auto-generated using the hiero project name", lambda keyword, task: generate_project_code(task, hiero.core.projects()[-1].name()))

ShotProcessorPreset.addUserResolveEntries = shot_addUserResolveEntries