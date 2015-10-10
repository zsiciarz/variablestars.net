module JdConverter where

import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (..)
import Signal
import String
import Time exposing (every, second)

import Astronomy exposing (JD, CustomDate, timeToJd, dateToJd, dateFromJd)
import Utils exposing (formatJD)


main =
    Signal.map
        (view actions.address)
        (Signal.foldp update initModel
            (Signal.merge tick actions.signal))


tick : Signal Action
tick = Signal.map (Tick << timeToJd) (every second)


type alias Model =
    { date : CustomDate
    , currentJD : JD
    , useCurrentJD: Bool
    }


initDate = { year = 0,  month = 0, day = 0, hour = 0, minute = 0, second = 0 }
initModel = { date = initDate, currentJD = 0, useCurrentJD = True }


type Action
    = SetNow
    | SetYear String
    | SetMonth String
    | SetDay String
    | SetHour String
    | SetMinute String
    | SetSecond String
    | SetJD String
    | Tick JD


actions : Signal.Mailbox Action
actions = Signal.mailbox SetNow


updateDateField : Model -> (CustomDate -> Int -> CustomDate) -> String -> Model
updateDateField model f value =
    case String.toInt value of
        Ok v -> { model | date <- f (model.date) v }
        Err _ -> model


update : Action -> Model -> Model
update action model =
    case action of
        SetYear value -> updateDateField model (\d v -> { d | year <- v }) value
        SetMonth value -> updateDateField model (\d v -> { d | month <- v - 1 }) value
        SetDay value -> updateDateField model (\d v -> { d | day <- v }) value
        SetHour value -> updateDateField model (\d v -> { d | hour <- v }) value
        SetMinute value -> updateDateField model (\d v -> { d | minute <- v }) value
        SetSecond value -> updateDateField model (\d v -> { d | second <- v }) value
        SetJD value -> case String.toFloat value of
            Ok value -> { model | date <- dateFromJd value }
            Err _ -> model
        Tick jd -> if model.useCurrentJD
            then { model | currentJD <- jd, date <- dateFromJd jd, useCurrentJD <- False }
            else { model | currentJD <- jd }
        SetNow -> { model | date <- dateFromJd (model.currentJD) }


calendarInput : Signal.Address Action -> Int -> (String -> Action) -> Html
calendarInput address modelValue action =
    input
        [ class "form-control"
        , type' "number"
        , value (toString modelValue)
        , on "input" targetValue (\str -> Signal.message address (action str))
        ]
        []


view : Signal.Address Action -> Model -> Html
view address model =
    div []
        [ label []
            [ text "Date and time (UTC) "
            , a [href "#", onClick address SetNow ] [ text "now" ]
            ]
        , div [ class "form-group row" ]
            [ div [ class "col-xs-2" ] [calendarInput address model.date.year SetYear]
            , div [ class "col-xs-2" ] [calendarInput address (model.date.month + 1) SetMonth]
            , div [ class "col-xs-2" ] [calendarInput address model.date.day SetDay]
            , div [ class "col-xs-2" ] [calendarInput address model.date.hour SetHour]
            , div [ class "col-xs-2" ] [calendarInput address model.date.minute SetMinute]
            , div [ class "col-xs-2" ] [calendarInput address model.date.second SetSecond]
            ],
        div [class "form-group" ]
            [ label [] [text "JD"]
            , input
                [ class "form-control"
                , value (formatJD 4 <| dateToJd model.date)
                , on "input" targetValue (\str -> Signal.message address (SetJD str))
                ]
                []
            ]
        ]
