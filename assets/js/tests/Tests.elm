module Tests where

import ElmTest exposing (..)

import AstronomyTests


all : Test
all =
    suite "variablestars.net tests"
        [
            AstronomyTests.tests
        ]
