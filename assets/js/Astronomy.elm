module Astronomy (JD, timeToJd, jdToTime) where

import Time exposing (Time)


type alias JD = Float


timeToJd : Time -> JD
timeToJd t =
    t / 86400000 + 2440587.5


jdToTime : JD -> Time
jdToTime jd =
    (jd - 2440587.5) * 86400000
