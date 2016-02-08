module Astronomy (JD, intToMonth, timeToJd, jdToTime, dateFromJd, dateToJd) where

import Date
import Date.Core exposing (monthList, monthToInt)
import Date.Utils exposing (dateFromFields)
import List exposing (drop, head)
import Maybe exposing (withDefault)
import Time exposing (Time)


type alias JD = Float


intToMonth : Int -> Date.Month
intToMonth m = head (drop (m - 1) monthList) |> withDefault Date.Jan


timeToJd : Time -> JD
timeToJd t =
    t / 86400000 + 2440587.5


jdToTime : JD -> Time
jdToTime jd =
    (jd - 2440587.5) * 86400000


dateFromJd : JD -> Date.Date
dateFromJd jd = jdToTime jd |> Date.fromTime


-- see https://en.wikipedia.org/wiki/Julian_day#Converting_Julian_or_Gregorian_calendar_date_to_Julian_Day_Number
-- TODO: fix timezone offsets
dateToJd : Date.Date -> JD
dateToJd date =
    let
        month' = monthToInt (Date.month date)
        a = (14 - month') // 12
        y = (Date.year date) + 4800 - a
        m = month' + 12 * a - 3
        fraction = (toFloat ((Date.hour date) - 12)) / 24 + (toFloat (Date.minute date)) / 1440 + (toFloat (Date.second date)) / 86400
    in fraction + toFloat
       ((Date.day date) + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045)

