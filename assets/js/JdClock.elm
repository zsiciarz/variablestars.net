module JdClock (..) where

import Html exposing (..)
import Html.Attributes exposing (..)
import Time exposing (Time, every, second)
import Astronomy exposing (timeToJd)
import Utils exposing (formatJD)


main =
  Signal.map jdClock (every second)


jdClock : Time -> Html
jdClock t =
  let
    jdText =
      t |> timeToJd |> formatJD 4
  in
    div
      []
      [ span [ class "glyphicon glyphicon-time" ] []
      , a
          [ href "#"
          , id "current-jd"
          , attribute "data-toggle" "modal"
          , attribute "data-target" "#jd-converter"
          ]
          [ text (" JD: " ++ jdText) ]
      ]
