from galaxy_morph import GalaxyMorph

galaxy_classifier = GalaxyMorph()
prediction = galaxy_classifier.predict("test.jpg")

print(prediction)
