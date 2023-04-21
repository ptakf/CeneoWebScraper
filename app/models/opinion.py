from app.parameters import selectors
from app.utils import get_item


class Opinion():
    """
    Opinion objects extract attributes related to opinions.

    Attributes:
        author -- author of the opinion (default: "")
        recommendation --  (default: None)
        stars -- amount of stars (default: 0)
        content -- content of the opinion (default: "")
        useful -- amount of the "useful" votes received (default: 0)
        useless -- amount of the "useless" votes received (default: 0)
        published -- publication date of the opinion (default: None)
        purchased -- purchase date of the product (default: None)
        pros -- list of the product's pros (default: [])
        cons -- list of the product's cons (default: [])
        opinion_id -- ID of the opinion (default: "")
    """

    def __init__(self, author="", recommendation=None, stars=0, content="", useful=0, useless=0,
                 published=None, purchased=None, pros=[], cons=[], opinion_id=""):
        """Initialize the Opinion object based on passed arguments."""
        self.author = author
        self.recommendation = recommendation
        self.stars = stars
        self.content = content
        self.useful = useful
        self.useless = useless
        self.published = published
        self.purchased = purchased
        self.pros = pros
        self.cons = cons
        self.opinion_id = opinion_id

    def __str__(self):
        """Return a human-readable string representation of the Opinion object."""
        return (f"opinion_id: {self.opinion_id}<br>"
                + "<br>".join(f"{key}: {str(getattr(self, key))}" for key in selectors.keys()))

    def __repr__(self):
        """Return a string representation of the Opinion object readable by the Python interpreter."""
        return (f"Opinion(opinion_id={self.opinion_id}, "
                + ", ".join(f"{key}={str(getattr(self, key))}" for key in selectors.keys()) + ")")

    def to_dict(self):
        """Return a dictionary of the Opinion object's attributes."""
        return {"opinion_id": self.opinion_id} | {key: getattr(self, key) for key in selectors.keys()}

    def extract_opinion(self, opinion):
        """
        Extract an opinion's attributes from an HTML element passed as an argument.
        Assign them to the Opinion object. Return the opinion.
        """
        for key, value in selectors.items():
            setattr(self, key, get_item(opinion, *value))
        self.opinion_id = opinion["data-entry-id"]
        return self
