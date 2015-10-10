module Utils (formatJD) where

import String


formatJD n x =
    case 10^n * x |> toString |> String.split "." of
        [s, _] -> (String.dropRight n s) ++ "." ++ (String.right n s)
        [s] -> s
        _ -> ""

