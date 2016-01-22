module AstronomyTests where

import ElmTest exposing (..)

import Astronomy exposing (timeToJd)


tests : Test
tests =
    suite "Astronomy module tests"
        [
            test "JD epoch" (assertEqual (timeToJd 0) 2440587.5)
        ]
