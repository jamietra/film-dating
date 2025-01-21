import exif
from datetime import datetime, timedelta
from pathlib import Path


class FilmSorter:
    def __init__(self, directory: Path):
        self.date = datetime.strptime(directory.name, "%Y-%m-%d").replace(hour=13)
        self.directory = directory
        outer_out_dir = Path("../../Pictures/sorted_march_2024")
        outer_out_dir.mkdir(exist_ok=True)
        self.out_dir = outer_out_dir / directory.name
        self.out_dir.mkdir(exist_ok=True)
        self.images = self.read_all_images(directory)
        self.add_ordered_datetime()
        self.save_all_images_as_modified()

    def read_all_images(self, directory: Path):
        files = directory.glob("*.jpg")
        image_dict = {}
        for f in sorted(files):
            with open(f, "rb") as fopen:
                image_file = fopen
                image_dict[f.name] = exif.Image(image_file)

        return image_dict

    def add_ordered_datetime(self):
        date = self.date
        for name in sorted(self.images.keys(), reverse=True):
            self.images[name].set("datetime", date.strftime("%Y:%m:%d %H:%M:%S"))
            date += timedelta(seconds=1)

    def save_all_images_as_modified(self):
        for name in sorted(self.images.keys()):
            with open(self.out_dir / name, "wb") as new_image_file:
                new_image_file.write(self.images[name].get_file())


def main():
    outer_dir = Path("../../Pictures/march_2024")
    for subdir in sorted(outer_dir.iterdir()):
        if subdir.name != ".DS_Store":
            FilmSorter(subdir)


if __name__ == "__main__":
    main()
