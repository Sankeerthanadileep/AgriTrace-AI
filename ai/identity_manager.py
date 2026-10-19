class IdentityManager:

    def __init__(self):
        self.animal_map = {}
        self.next_animal_id = 1

    def get_animal_id(self, tracking_id):

        tracking_id = str(tracking_id)

        if tracking_id not in self.animal_map:

            self.animal_map[tracking_id] = (
                f"COW-{self.next_animal_id:03d}"
            )

            self.next_animal_id += 1

        return self.animal_map[tracking_id]


if __name__ == "__main__":

    manager = IdentityManager()

    print(manager.get_animal_id(1))
    print(manager.get_animal_id(2))
    print(manager.get_animal_id(1))
    print(manager.get_animal_id(5))