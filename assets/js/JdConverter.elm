module JdConverter where

import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (..)
import Date
import String
import StartApp.Simple

import Astronomy exposing (JD, timeToJd, jdToTime)

main =
    StartApp.Simple.start { model = initModel, update = update, view = view }


type alias Model =
    { year : Int
    , month: Int
    , day: Int
    , hour: Int
    , minute: Int
    , second: Int
    }


initModel = { year = 0,  month = 0, day = 0, hour = 0, minute = 0, second = 0 }


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


modelFromJd : JD -> Model
modelFromJd jd =
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


modelToJd : Model -> JD
modelToJd model =
    666.0


type Action a
    = SetYear a
    | SetMonth a
    | SetDay a
    | SetHour a
    | SetMinute a
    | SetSecond a
    | SetJD a


update : Action String -> Model -> Model
update action model =
    case action of
        SetYear value -> case String.toInt value of
            Ok value -> { model | year <- value }
            Err _ -> model
        SetMonth value -> case String.toInt value of
            Ok value -> { model | month <- value }
            Err _ -> model
        SetDay value -> case String.toInt value of
            Ok value -> { model | day <- value }
            Err _ -> model
        SetHour value -> case String.toInt value of
            Ok value -> { model | hour <- value }
            Err _ -> model
        SetMinute value -> case String.toInt value of
            Ok value -> { model | minute <- value }
            Err _ -> model
        SetSecond value -> case String.toInt value of
            Ok value -> { model | second <- value }
            Err _ -> model
        SetJD value -> case String.toFloat value of
            Ok value -> modelFromJd value
            Err _ -> model


calendarInput : Signal.Address (Action String) -> Int -> (String -> Action String) -> Html
calendarInput address modelValue action =
    input
        [ class "form-control"
        , type' "number"
        , value (toString modelValue)
        , on "input" targetValue (\str -> Signal.message address (action str))
        ]
        []


view : Signal.Address (Action String) -> Model -> Html
view address model =
    div []
        [ text (toString model)
        , calendarInput address model.year SetYear
        , calendarInput address model.month SetMonth
        , calendarInput address model.day SetDay
        , calendarInput address model.hour SetHour
        , calendarInput address model.minute SetMinute
        , calendarInput address model.second SetSecond
        , input
            [ class "form-control"
            , value (toString <| modelToJd model)
            , on "input" targetValue (\str -> Signal.message address (SetJD str))
            ]
            []
        ]
