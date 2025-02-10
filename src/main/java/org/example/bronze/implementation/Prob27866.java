package org.example.bronze.implementation;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Prob27866 {
    public static void main(String[] args) throws IOException {
        BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
        String word = reader.readLine();
        int number = Integer.parseInt(reader.readLine());

        System.out.println(word.charAt(number - 1));

        reader.close();
    }
}
