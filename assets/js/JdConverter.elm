module JdConverter exposing (..)

import Date exposing (Date, Month)
import Date.Extra.Core exposing (monthToInt)
import Date.Extra.Create exposing (dateFromFields)
import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (..)
import Json.Decode
import String
import Time exposing (every, second)
import Astronomy exposing (JD, timeToJd, dateToJd, dateFromJd, intToMonth)
import Utils exposing (formatJD)


--port timezoneOffset : Float


timezoneOffset =
    0.0


main =
    Html.program
        { init = init
        , view = view
        , update = update
        , subscriptions = tick
        }


tick : Model -> Sub Msg
tick model =
    every second (Tick << (\time -> timeToJd time + timezoneOffset))


type alias Model =
    { date : Date
    , currentJD : JD
    , useCurrentJD : Bool
    }


initDate =
    dateFromFields 0 Date.Jan 0 0 0 0 0


init : ( Model, Cmd Msg )
init =
    ( { date = initDate, currentJD = 0, useCurrentJD = True }, Cmd.none )


type Msg
    = SetNow
    | SetYear String
    | SetMonth String
    | SetDay String
    | SetHour String
    | SetMinute String
    | SetSecond String
    | SetJD String
    | Tick JD


updateDateField : Msg -> String -> Model -> ( Model, Cmd Msg )
updateDateField msg value model =
    let
        f msg d v =
            case msg of
                SetYear _ ->
                    dateFromFields v (Date.month d) (Date.day d) (Date.hour d) (Date.minute d) (Date.second d) 0

                SetMonth _ ->
                    dateFromFields (Date.year d) (intToMonth v) (Date.day d) (Date.hour d) (Date.minute d) (Date.second d) 0

                SetDay _ ->
                    dateFromFields (Date.year d) (Date.month d) v (Date.hour d) (Date.minute d) (Date.second d) 0

                SetHour _ ->
                    dateFromFields (Date.year d) (Date.month d) (Date.day d) v (Date.minute d) (Date.second d) 0

                SetMinute _ ->
                    dateFromFields (Date.year d) (Date.month d) (Date.day d) (Date.hour d) v (Date.second d) 0

                SetSecond _ ->
                    dateFromFields (Date.year d) (Date.month d) (Date.day d) (Date.hour d) (Date.minute d) v 0

                _ ->
                    d
    in
        case String.toInt value of
            Ok v ->
                ( { model | date = f msg (model.date) v }, Cmd.none )

            Err _ ->
                ( model, Cmd.none )


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        SetYear value ->
            updateDateField msg value model

        SetMonth value ->
            updateDateField msg value model

        SetDay value ->
            updateDateField msg value model

        SetHour value ->
            updateDateField msg value model

        SetMinute value ->
            updateDateField msg value model

        SetSecond value ->
            updateDateField msg value model

        SetJD value ->
            case String.toFloat value of
                Ok value ->
                    ( { model | date = dateFromJd (value + timezoneOffset / 86400000) }, Cmd.none )

                Err _ ->
                    ( model, Cmd.none )

        Tick jd ->
            if model.useCurrentJD then
                ( { model | currentJD = jd, date = dateFromJd jd, useCurrentJD = False }, Cmd.none )
            else
                ( { model | currentJD = jd }, Cmd.none )

        SetNow ->
            ( { model | date = dateFromJd (model.currentJD) }, Cmd.none )


calendarInput : Int -> (String -> Msg) -> Html Msg
calendarInput modelValue msg =
    input
        [ class "form-control"
        , type_ "number"
        , value (toString modelValue)
        , onInput msg
        ]
        []


view : Model -> Html Msg
view model =
    div []
        [ label []
            [ text "Date and time (UTC) "
            , a [ href "#", onClick SetNow ] [ text "now" ]
            ]
        , div [ class "form-group row" ]
            [ div [ class "col-xs-2" ] [ calendarInput (Date.year model.date) SetYear ]
            , div [ class "col-xs-2" ] [ calendarInput (monthToInt (Date.month model.date)) SetMonth ]
            , div [ class "col-xs-2" ] [ calendarInput (Date.day model.date) SetDay ]
            , div [ class "col-xs-2" ] [ calendarInput (Date.hour model.date) SetHour ]
            , div [ class "col-xs-2" ] [ calendarInput (Date.minute model.date) SetMinute ]
            , div [ class "col-xs-2" ] [ calendarInput (Date.second model.date) SetSecond ]
            ]
        , div [ class "form-group" ]
            [ label [] [ text "JD" ]
            , input
                [ class "form-control"
                , value (dateToJd model.date |> formatJD)
                , onInput SetJD
                ]
                []
            ]
        ]
