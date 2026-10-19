import math


class AppearanceIdentityManager:

    def __init__(self, max_distance=120):

        self.animals = {}

        self.next_animal_number = 1

        self.max_distance = max_distance


    def _distance(self, point1, point2):

        x1, y1 = point1
        x2, y2 = point2

        return math.sqrt(
            (x2 - x1) ** 2
            +
            (y2 - y1) ** 2
        )


    def register_animal(
        self,
        tracking_id,
        center
    ):

        animal_id = (
            f"ANIMAL-{self.next_animal_number:03d}"
        )

        self.next_animal_number += 1

        self.animals[animal_id] = {

            "tracking_id": str(tracking_id),

            "last_center": center,

            "frames_seen": 1
        }

        return animal_id


    def find_existing_animal(
        self,
        center
    ):

        best_animal = None

        best_distance = float("inf")


        for animal_id, data in self.animals.items():

            previous_center = data["last_center"]

            distance = self._distance(
                center,
                previous_center
            )


            if distance < best_distance:

                best_distance = distance

                best_animal = animal_id


        if (
            best_animal is not None
            and best_distance <= self.max_distance
        ):

            return best_animal


        return None


    def update_animal(
        self,
        animal_id,
        tracking_id,
        center
    ):

        self.animals[animal_id][
            "tracking_id"
        ] = str(tracking_id)

        self.animals[animal_id][
            "last_center"
        ] = center

        self.animals[animal_id][
            "frames_seen"
        ] += 1


    def get_or_create(
        self,
        tracking_id,
        center
    ):

        # First check whether this tracking ID
        # is already connected to an animal.

        for animal_id, data in self.animals.items():

            if data["tracking_id"] == str(tracking_id):

                self.update_animal(
                    animal_id,
                    tracking_id,
                    center
                )

                return animal_id


        # Tracking ID is new.
        # Try to match it with an existing animal
        # based on its previous position.

        existing_animal = self.find_existing_animal(
            center
        )


        if existing_animal is not None:

            self.update_animal(
                existing_animal,
                tracking_id,
                center
            )

            return existing_animal


        # No match found.
        # Create a new animal.

        return self.register_animal(
            tracking_id,
            center
        )


if __name__ == "__main__":

    manager = AppearanceIdentityManager()

    animal1 = manager.get_or_create(
        1,
        (100, 100)
    )

    print(
        "First detection:",
        animal1
    )


    animal1_again = manager.get_or_create(
        1,
        (105, 103)
    )

    print(
        "Same tracking ID:",
        animal1_again
    )


    animal1_reappears = manager.get_or_create(
        55,
        (110, 105)
    )

    print(
        "New tracking ID, nearby:",
        animal1_reappears
    )


    animal2 = manager.get_or_create(
        2,
        (500, 500)
    )

    print(
        "Different animal:",
        animal2
    )