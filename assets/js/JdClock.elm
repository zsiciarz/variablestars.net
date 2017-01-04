module JdClock exposing (..)

import Html exposing (..)
import Html.Attributes exposing (..)
import Time exposing (Time, every, second)
import Astronomy exposing (timeToJd)
import Utils exposing (formatJD)


main =
    Html.program
        { init = ( 0, Cmd.none )
        , update = update
        , view = view
        , subscriptions = subscriptions
        }


subscriptions : Model -> Sub Msg
subscriptions model =
    every second Tick


type alias Model =
    Time


type Msg
    = Tick Time


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        Tick time ->
            ( time, Cmd.none )


view : Time -> Html a
view t =
    let
        jdText =
            t |> timeToJd |> formatJD
    in
        div []
            [ span [ class "glyphicon glyphicon-time" ] []
            , a
                [ href "#"
                , id "current-jd"
                , attribute "data-toggle" "modal"
                , attribute "data-target" "#jd-converter"
                ]
                [ text (" JD: " ++ jdText) ]
            ]
