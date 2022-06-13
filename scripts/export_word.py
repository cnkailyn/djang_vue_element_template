import os

import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

from apps.main.models import WordGroup, KeyWord


if __name__ == "__main__":
    current_path = os.getcwd()
    WordGroup.objects.all().delete()
    KeyWord.objects.all().delete()

    for file_ in os.listdir("words"):
        if not file_.endswith("txt"):
            continue

        group_name = file_.split(".")[0]
        group = WordGroup(name=group_name)
        group.save()
        keys = []
        with open(os.path.join(current_path, "words", file_), "r", encoding="utf-8") as f:
            for i in f:
                if not i.strip():
                    continue
                keys.append(KeyWord(word=i.strip(), group=group))
        KeyWord.objects.bulk_create(keys)
