class TagIdentityManager:

    def __init__(self):
        self.tracking_to_tag = {}
        self.tag_to_tracking = {}

    def register_tag(self, tracking_id, tag_id):

        tracking_id = str(tracking_id)
        tag_id = str(tag_id)

        self.tracking_to_tag[tracking_id] = tag_id
        self.tag_to_tracking[tag_id] = tracking_id

        return tag_id

    def get_tag(self, tracking_id):

        tracking_id = str(tracking_id)

        return self.tracking_to_tag.get(
            tracking_id
        )

    def get_tracking_id(self, tag_id):

        tag_id = str(tag_id)

        return self.tag_to_tracking.get(
            tag_id
        )

    def is_registered(self, tag_id):

        return tag_id in self.tag_to_tracking


if __name__ == "__main__":

    manager = TagIdentityManager()

    manager.register_tag(
        17,
        "COW-004"
    )

    manager.register_tag(
        23,
        "COW-007"
    )

    print(
        "Tracking 17:",
        manager.get_tag(17)
    )

    print(
        "Tracking 23:",
        manager.get_tag(23)
    )

    print(
        "COW-004 tracking:",
        manager.get_tracking_id("COW-004")
    )

    print(
        "COW-007 registered:",
        manager.is_registered("COW-007")
    )