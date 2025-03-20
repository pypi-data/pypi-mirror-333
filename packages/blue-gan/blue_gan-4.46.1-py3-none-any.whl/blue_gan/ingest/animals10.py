import glob
from tqdm import tqdm

from blueness import module
from blue_objects import objects, file
from blue_objects.metadata import post_to_object

from blue_gan import NAME
from blue_gan.logger import logger

NAME = module.name(__file__, NAME)

# https://www.kaggle.com/datasets/alessiocorrado99/animals10
translate = {
    "cane": "dog",
    "cavallo": "horse",
    "elefante": "elephant",
    "farfalla": "butterfly",
    "gallina": "chicken",
    "gatto": "cat",
    "mucca": "cow",
    "pecora": "sheep",
    "scoiattolo": "squirrel",
    "dog": "cane",
    "elephant": "elefante",
    "butterfly": "farfalla",
    "chicken": "gallina",
    "cat": "gatto",
    "cow": "mucca",
    "spider": "ragno",
    "squirrel": "scoiattolo",
}


def ingest(
    animal: str,
    cache_object_name: str,
    object_name: str,
    count: int = 10,
) -> bool:
    logger.info(
        "{}.ingest: {}/{} -count={}-> {}".format(
            NAME,
            cache_object_name,
            animal,
            count,
            object_name,
        )
    )

    animal_it = ([key for key, value in translate.items() if value == animal] + [""])[0]
    if not animal_it:
        logger.error(f"{animal}: animal not found.")
        return False
    logger.info(f"{animal} -🇮🇹 -> {animal_it}")

    count_copied = 0
    for filename in tqdm(
        glob.glob(
            objects.path_of(
                object_name=cache_object_name,
                filename=f"raw-img/{animal_it}/*.jpeg",
            )
        )
    ):
        if not file.copy(
            filename,
            objects.path_of(
                object_name=object_name,
                filename=file.name_and_extension(filename),
            ),
            log=True,
        ):
            return False

        count_copied += 1
        if count != -1 and count_copied >= count:
            break

    return post_to_object(
        object_name,
        NAME.replace(".", "_"),
        {
            "animal": animal,
            "animal_it": animal_it,
            "cache_object_name": cache_object_name,
            "count": count_copied,
        },
    )
