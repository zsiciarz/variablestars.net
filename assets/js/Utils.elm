module Utils (formatJD) where

import String
import Number.Format exposing (pretty)


formatJD n x =
  pretty n ' ' x |> String.filter (\c -> c /= ' ')
