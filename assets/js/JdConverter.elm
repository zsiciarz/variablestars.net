module JdConverter where

import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (..)
import String
import StartApp.Simple

import Astronomy exposing (JD, timeToJd, jdToTime)

main =
    StartApp.Simple.start { model = 0.0, update = update, view = view }


type alias Model = JD


type Action a
    = NoOp
    | SetJD a


update : Action String -> Model -> Model
update action model =
    case action of
        NoOp -> model
        SetJD value -> case String.toFloat value of
            Ok jd -> jd
            Err _ -> 0.0


view : Signal.Address (Action String) -> Model -> Html
view address model =
    div []
        [ text (toString model)
        , input
            [ class "form-control"
            , value (toString model)
            , on "input" targetValue (\str -> Signal.message address (SetJD str))
            ]
            []
        ]
