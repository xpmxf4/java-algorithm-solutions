    package org.example.bronze.implementation;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Arrays;

public class Prob2475 {
    public static void main(String[] args) throws IOException {
        // input
        BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
        String input = reader.readLine();
        int[] numbers = Arrays.stream(input.split(" "))
                .mapToInt(Integer::parseInt).toArray();
        int answer;


        // logic
        int sum = 0;
        for (int number : numbers)
            sum += (int) Math.pow(number, 2);
        answer = sum % 10;

        // output
        System.out.println(answer);
    }
}
