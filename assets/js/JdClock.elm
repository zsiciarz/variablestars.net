module JdClock where

import Html exposing (..)
import Html.Attributes exposing (..)
import Time exposing (Time, every, second)


type alias JD = Float


main =
  Signal.map jdClock (every second)


timeToJd : Time -> JD
timeToJd t =
    t / 86400000 + 2440587.5


jdClock : Time -> Html
jdClock t =
    let
        jdText = t |> timeToJd |> toString
    in
        div []
            [ span [class "glyphicon glyphicon-time"] []
            , a [ href "#"
                , id "current-jd"
                , attribute "data-toggle" "modal"
                , attribute "data-target" "#jd-converter"
                ]
                [text (" JD: " ++ jdText)]
            ]
