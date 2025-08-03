module Main where

import Text.Read

main = do
    putStrLn "Enter the factorial: "
    input <- getLine
    case readMaybe input of
        Just a -> case factorial a of
            Just x -> print x
            _ -> putStrLn "Only +ve ints supported"
        Nothing -> putStrLn "Invalid Input"
    --case factorial (read input :: Integer) of
    --    Just a -> print a
    --    Nothing -> putStrLn "Invalid Input"

factorial :: Integer -> (Maybe Integer)
factorial n = if n < 0 then Nothing else Just (factorial' n)
factorial' x
    | x == 0 = 1
    | otherwise = x * factorial' (x - 1)
