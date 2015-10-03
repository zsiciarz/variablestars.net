module JdClock where

import Html exposing (..)
import Html.Attributes exposing (..)
import String
import Time exposing (Time, every, second)

import Astronomy exposing (timeToJd)

main =
  Signal.map jdClock (every second)

formatJD n x =
    let
        [s, _] = 10^n * x |> toString |> String.split "."
        p1 = String.dropRight n s
        p2 = String.right n s
    in
        p1 ++ "." ++ p2

jdClock : Time -> Html
jdClock t =
    let
        jdText = t |>  timeToJd |> formatJD 4
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
