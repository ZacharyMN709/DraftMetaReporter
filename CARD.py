class CardFace():

    def __init__(self, json):
        pass



class Card():

    def __init__(self, json):
        if json['object'] != 'card':
            raise Exception("Invalid JSON provided.")

        self._FACE_FRONT = CardFace()
        self._FACE_BACK = CardFace()


