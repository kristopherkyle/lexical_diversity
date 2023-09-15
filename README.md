# To install using pip:

    pip install lexical-diversity

# Get started:

    >>> from lexical_diversity import lex_div as ld

# Pre-processing texts:
For convenience, a user can tokenize texts using the **tokenize()** function or by using a predefined tokenize function (e.g., from NLTK):

    >>> text = """The state was named for the Colorado River, which Spanish travelers named the Río Colorado for the ruddy silt the river carried from the mountains. The Territory of Colorado was organized on February 28, 1861, and on August 1, 1876, U.S. President Ulysses S. Grant signed Proclamation 230 admitting Colorado to the Union as the 38th state. Colorado is nicknamed the "Centennial State" because it became a state a century after the signing of the United States Declaration of Independence. Colorado is bordered by Wyoming to the north, Nebraska to the northeast, Kansas to the east, Oklahoma to the southeast, New Mexico to the south, Utah to the west, and touches Arizona to the southwest at the Four Corners. Colorado is noted for its vivid landscape of mountains, forests, high plains, mesas, canyons, plateaus, rivers, and desert lands. Colorado is part of the western or southwestern United States, and one of the Mountain States. Denver is the capital and most populous city of Colorado. Residents of the state are known as Coloradans, although the antiquated term "Coloradoan" is occasionally used."""

    >>> tok = ld.tokenize(text)
    >>> print(tok[:10])
    ['the', 'state', 'was', 'named', 'for', 'the', 'colorado', 'river', 'which', 'spanish']

For convenience, you can also lemmatize the texts using the simple **flemmatize()** function, which is not part of speech specific ('run' as a noun and 'run' as a verb are treated as the same word). However, it is likely better to use a part of speech sensitive lemmatizer (e.g., using spaCy).

    >>> flt = ld.flemmatize(text)
    >>> print(flt[:10])
    ['the', 'state', 'be', 'name', 'for', 'the', 'colorado', 'river', 'which', 'spanish']  

# Calculating lexical diversity:

## Recommended indices:

## Classic (but not recommended) indices:

### Simple TTR
Simple TTR is the worst thing you could ever use. Here is why. It is calculated as (blah blah blah). See here for more information.

    >>> ld.ttr(flt)
    0.5777777777777777

### Root TTR

    >>> ld.root_ttr(flt)
    7.751702321999271

### Log TTR

    >>> ld.log_ttr(flt)
    0.8943634681549878

### Maas TTR

    >>> ld.maas_ttr(flt)
    0.04683980831849556

### Mean segmental TTR (MSTTR)
By default, the segment size is 50 words. However, this can be customized using the *window_length* argument.

    >>> ld.msttr(flt)
    0.7133333333333333

    >>> ld.msttr(flt,window_length=25)
    0.7885714285714285

### Moving average TTR (MATTR)
By default, the window size is 50 words. However, this can be customized using the *window_length* argument.

    >>> ld.mattr(flt)
    0.7206106870229007

    >>> ld.mattr(flt,window_length=25)
    0.7961538461538458

### Hypergeometric distribution D (HDD)
A more straightforward and reliable implementation of vocD (Malvern, Richards, Chipere, & Duran, 2004) as per McCarthy and Jarvis (2007, 2010).

    >>> ld.hdd(flt)
    0.7346993253061275

### Measure of lexical textual diversity (MTLD)
Calculates MTLD based on McCarthy and Jarvis (2010).

    ld.mtld(flt)
    36.50595044690307

### Measure of lexical textual diversity (moving average, wrap)
Calculates MTLD using a moving window approach. Instead of calculating partial factors, it wraps to the beginning of the text to complete the last factors.

    ld.mtld_ma_wrap(flt)
    33.68333333333333

### Measure of lexical textual diversity (moving average, bi-directional)
Calculates the average MTLD score by calculating MTLD in each direction using a moving window approach.

    ld.mtld_ma_bid(flt)
    35.46626265150569
