package org.example;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Arrays;

public class Main {
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