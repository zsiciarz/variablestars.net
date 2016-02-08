module JdConverter where

import Date exposing (Date, Month)
import Date.Core exposing (monthToInt)
import Date.Utils exposing (dateFromFields)
import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (..)
import Signal
import String
import Time exposing (every, second)

import Astronomy exposing (JD, timeToJd, dateToJd, dateFromJd, intToMonth)
import Utils exposing (formatJD)


port timezoneOffset : Float


main =
    Signal.map
        (view actions.address)
        (Signal.foldp update initModel
            (Signal.merge tick actions.signal))


tick : Signal Action
tick =
    let
        localClock = (Signal.map (\time -> time + timezoneOffset) (every second))
    in
        Signal.map (Tick << timeToJd) localClock


type alias Model =
    { date : Date
    , currentJD : JD
    , useCurrentJD: Bool
    }


initDate = dateFromFields 0 Date.Jan 0 0 0 0 0
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


updateDateField : Action -> String -> Model -> Model
updateDateField action value model =
    let
        f action d v = case action of
            (SetYear _) -> dateFromFields v (Date.month d) (Date.day d) (Date.hour d) (Date.minute d) (Date.second d) 0
            (SetMonth _) -> dateFromFields (Date.year d) (intToMonth v) (Date.day d) (Date.hour d) (Date.minute d) (Date.second d) 0
            (SetDay _) -> dateFromFields (Date.year d) (Date.month d) v (Date.hour d) (Date.minute d) (Date.second d) 0
            (SetHour _) -> dateFromFields (Date.year d) (Date.month d) (Date.day d) v (Date.minute d) (Date.second d) 0
            (SetMinute _) -> dateFromFields (Date.year d) (Date.month d) (Date.day d) (Date.hour d) v (Date.second d) 0
            (SetSecond _) -> dateFromFields (Date.year d) (Date.month d) (Date.day d) (Date.hour d) (Date.minute d) v 0
            _ -> d
    in
        case String.toInt value of
            Ok v -> { model | date = f action (model.date) v }
            Err _ -> model


update : Action -> Model -> Model
update action model =
    case action of
        SetYear value -> updateDateField action value model
        SetMonth value -> updateDateField action value model
        SetDay value -> updateDateField action value model
        SetHour value -> updateDateField action value model
        SetMinute value -> updateDateField action value model
        SetSecond value -> updateDateField action value model
        SetJD value -> case String.toFloat value of
            Ok value -> { model | date = dateFromJd (value + timezoneOffset / 86400000) }
            Err _ -> model
        Tick jd -> if model.useCurrentJD
            then { model | currentJD = jd, date = dateFromJd jd, useCurrentJD = False }
            else { model | currentJD = jd }
        SetNow -> { model | date = dateFromJd (model.currentJD) }


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
            [ div [ class "col-xs-2" ] [calendarInput address (Date.year model.date) SetYear]
            , div [ class "col-xs-2" ] [calendarInput address (monthToInt (Date.month model.date)) SetMonth]
            , div [ class "col-xs-2" ] [calendarInput address (Date.day model.date) SetDay]
            , div [ class "col-xs-2" ] [calendarInput address (Date.hour model.date) SetHour]
            , div [ class "col-xs-2" ] [calendarInput address (Date.minute model.date) SetMinute]
            , div [ class "col-xs-2" ] [calendarInput address (Date.second model.date) SetSecond]
            ],
        div [class "form-group" ]
            [ label [] [text "JD"]
            , input
                [ class "form-control"
                , value (dateToJd model.date |> formatJD 4)
                , on "input" targetValue (\str -> Signal.message address (SetJD str))
                ]
                []
            ]
        ]
