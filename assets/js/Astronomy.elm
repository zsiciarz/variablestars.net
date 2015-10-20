module Astronomy (JD, CustomDate, timeToJd, jdToTime, dateFromJd, dateToJd) where

import Date
import Time exposing (Time)


type alias JD = Float


timeToJd : Time -> JD
timeToJd t =
    t / 86400000 + 2440587.5


jdToTime : JD -> Time
jdToTime jd =
    (jd - 2440587.5) * 86400000


type alias CustomDate =
    { year : Int
    , month: Int
    , day: Int
    , hour: Int
    , minute: Int
    , second: Int
    }


monthLookup : Date.Month -> Int
monthLookup month =
    case month of
        Date.Jan -> 0
        Date.Feb -> 1
        Date.Mar -> 2
        Date.Apr -> 3
        Date.May -> 4
        Date.Jun -> 5
        Date.Jul -> 6
        Date.Aug -> 7
        Date.Sep -> 8
        Date.Oct -> 9
        Date.Nov -> 10
        Date.Dec -> 11


dateFromJd : JD -> CustomDate
dateFromJd jd =
    let
        d = jdToTime jd |> Date.fromTime
    in
        { year = Date.year d
        , month = monthLookup (Date.month d)
        , day = Date.day d
        , hour = Date.hour d
        , minute = Date.minute d
        , second = Date.second d
        }


-- see https://en.wikipedia.org/wiki/Julian_day#Converting_Julian_or_Gregorian_calendar_date_to_Julian_Day_Number
-- TODO: fix timezone offsets
dateToJd : CustomDate -> JD
dateToJd date =
    let
        month' = date.month + 1
        a = (14 - month') // 12
        y = date.year + 4800 - a
        m = month' + 12 * a - 3
        fraction = (toFloat (date.hour - 12)) / 24 + (toFloat date.minute) / 1440 + (toFloat date.second) / 86400
    in fraction + toFloat
       (date.day + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045)

