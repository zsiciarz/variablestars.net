module Astronomy (JD, timeToJd) where

import Time exposing (Time)


type alias JD = Float


timeToJd : Time -> JD
timeToJd t =
    t / 86400000 + 2440587.5
