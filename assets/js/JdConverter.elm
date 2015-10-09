module JdConverter where

import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (..)
import String
import StartApp.Simple

import Astronomy exposing (JD, CustomDate, timeToJd, jdToTime, dateToJd, dateFromJd)

main =
    StartApp.Simple.start { model = initModel, update = update, view = view }


type alias Model = CustomDate


initModel = { year = 0,  month = 0, day = 0, hour = 0, minute = 0, second = 0 }


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
            Ok value -> dateFromJd value
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
        , label [] [text "Date and time (UTC)"]
        , div [ class "form-group row" ]
            [ div [ class "col-xs-2" ] [calendarInput address model.year SetYear]
            , div [ class "col-xs-2" ] [calendarInput address model.month SetMonth]
            , div [ class "col-xs-2" ] [calendarInput address model.day SetDay]
            , div [ class "col-xs-2" ] [calendarInput address model.hour SetHour]
            , div [ class "col-xs-2" ] [calendarInput address model.minute SetMinute]
            , div [ class "col-xs-2" ] [calendarInput address model.second SetSecond]
            ],
        div [class "form-group" ]
            [ label [] [text "JD"]
            , input
                [ class "form-control"
                , value (toString <| dateToJd model)
                , on "input" targetValue (\str -> Signal.message address (SetJD str))
                ]
                []
            ]
        ]
