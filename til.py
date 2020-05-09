'''TIL - today I learned ...
'''

from pathlib import Path

class TodayILearned():

    def __init__(self):
        self.PROJECT_DIR = Path.cwd()
        super().__init__()


    def create(self, til_topic, til_name, til_type):
        if til_type == 'private':
            TOPIC_DIR = self.PROJECT_DIR / 'private'
        else:
            TOPIC_DIR = self.PROJECT_DIR / '{}'.format(til_topic)

        if not TOPIC_DIR.exists():
            TOPIC_DIR.mkdir(parents=True, exist_ok=True)

        TIL_FILE = TOPIC_DIR / '{}'.format(til_name)

        if TIL_FILE.exists():
            print('{} exists'.format(TIL_FILE))
        else:
            TIL_FILE.touch()
            print('Created {}'.format(TIL_FILE))

        return


    def sync(self):
        pass
