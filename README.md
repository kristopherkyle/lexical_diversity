# To install using pip:

    pip install lexical-diversity

# Get started:

    >>> from lexical_diversity import lex_div as ld
    
# Processing texts:
You can tokenize texts using the tokenize() function:

   >>> text = """The state was named for the Colorado River, which Spanish travelers named the Río Colorado for the ruddy silt the river carried from the mountains. The Territory of Colorado was organized on February 28, 1861, and on August 1, 1876, U.S. President Ulysses S. Grant signed Proclamation 230 admitting Colorado to the Union as the 38th state. Colorado is nicknamed the "Centennial State" because it became a state a century after the signing of the United States Declaration of Independence. Colorado is bordered by Wyoming to the north, Nebraska to the northeast, Kansas to the east, Oklahoma to the southeast, New Mexico to the south, Utah to the west, and touches Arizona to the southwest at the Four Corners. Colorado is noted for its vivid landscape of mountains, forests, high plains, mesas, canyons, plateaus, rivers, and desert lands. Colorado is part of the western or southwestern United States, and one of the Mountain States. Denver is the capital and most populous city of Colorado. Residents of the state are known as Coloradans, although the antiquated term "Coloradoan" is occasionally used."""
   
   >>> tok = ld.tokenize(text)
   >>> print(tok[:10])
['the', 'state', 'was', 'named', 'for', 'the', 'colorado', 'river', 'which', 'spanish']
   

