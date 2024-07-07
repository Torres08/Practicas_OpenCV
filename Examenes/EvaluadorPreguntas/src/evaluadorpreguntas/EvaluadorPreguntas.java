/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Main.java to edit this template
 */
package evaluadorpreguntas;

/**
 *
 * @author juanm
 */
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Scanner;

public class EvaluadorPreguntas {

    static class Pregunta {
        String enunciado;
        String[] opciones;
        char solucion;

        Pregunta(String enunciado, String[] opciones, char solucion) {
            this.enunciado = enunciado;
            this.opciones = opciones;
            this.solucion = solucion;
        }
    }

    public static void main(String[] args) {
        ArrayList<Pregunta> preguntas = new ArrayList<>();
        String archivo = "questions_corrected.txt";

        try (BufferedReader br = new BufferedReader(new FileReader(archivo))) {
            String linea;
            while ((linea = br.readLine()) != null) {
                if (linea.matches("\\d+\\. .*")) {
                    String enunciado = linea;
                    String[] opciones = new String[4];
                    for (int i = 0; i < 4; i++) {
                        opciones[i] = br.readLine().trim();
                    }
                    String solucionLinea = br.readLine().trim();
                    if (solucionLinea != null && solucionLinea.startsWith("Solución: ")) {
                        char solucion = solucionLinea.charAt(solucionLinea.length() - 1);
                        preguntas.add(new Pregunta(enunciado, opciones, solucion));
                    } else {
                        System.out.println("Formato incorrecto en la solución: " + solucionLinea);
                    }
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }

        Scanner scanner = new Scanner(System.in);
        int puntuacion = 0;
        int preguntasRealizadas = 0;
        int preguntasAcertadas = 0;

        for (Pregunta pregunta : preguntas) {
            imprimirConSaltosDeLinea(pregunta.enunciado, 100);
            for (String opcion : pregunta.opciones) {
                imprimirConSaltosDeLinea(opcion, 100);
            }
            System.out.print("Tu respuesta: ");
            char respuesta = scanner.next().charAt(0);

            preguntasRealizadas++;

            if (respuesta == pregunta.solucion) {
                puntuacion++;
                preguntasAcertadas++;
                System.out.println("¡Correcto!");
            } else {
                puntuacion--;
                System.out.println("Incorrecto. La respuesta correcta es: " + pregunta.solucion);
            }

            System.out.println("Preguntas acertadas: " + preguntasAcertadas + "/" + preguntasRealizadas);
            System.out.println();
        }

        System.out.println("Tu puntuación final es: " + puntuacion);
    }

    private static void imprimirConSaltosDeLinea(String texto, int longitudMax) {
        String[] palabras = texto.split(" ");
        StringBuilder lineaActual = new StringBuilder();

        for (String palabra : palabras) {
            if (lineaActual.length() + palabra.length() + 1 > longitudMax) {
                System.out.println(lineaActual.toString().trim());
                lineaActual = new StringBuilder();
            }
            lineaActual.append(palabra).append(" ");
        }
        System.out.println(lineaActual.toString().trim());
    }
}



