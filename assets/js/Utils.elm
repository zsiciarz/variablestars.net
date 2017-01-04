module Utils exposing (formatJD)

import Numeral exposing (format)


formatJD x =
    format "0.0000" x
