//-----------------------------------------------------
// Projeto: Desenvolvimento de API com Java Spring Boot
// Autora: Maria Fernanda Bronzoni
// RU: 4828466
//------------------------------------------------------

package com.uninter_java.api.config;

import java.sql.Connection;
import javax.sql.DataSource;

import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.stereotype.Component;

import com.uninter_java.api.controller.TarefaController;

@Component
public class Message implements ApplicationRunner {

    // Códigos de cores para console
    public static final String ANSI_RESET = "\u001B[0m";
    public static final String ANSI_PINK = "\u001B[95m";
    public static final String ANSI_RED = "\u001B[31m";
    public static final String ANSI_YELLOW = "\u001B[33m";
    public static final String ANSI_GREEN = "\u001B[32m";

    private final DataSource dataSource;
    private final TarefaController tarefaController;

    // Injeção de dependências
    public Message(DataSource dataSource, TarefaController tarefaController) {
        this.dataSource = dataSource;
        this.tarefaController = tarefaController;
    }

    @Override
    public void run(ApplicationArguments args) throws Exception {
        System.out.println("\n--- INICIANDO VALIDAÇÃO... ---");

        boolean dbOk = validarConexaoBanco();
        boolean apiOk = validarControllerAPI();

        imprimirBanner(dbOk, apiOk);
    }

    // Valida a conexão com o Banco de Dados
    private boolean validarConexaoBanco() {
        System.out.print(">> Validando conexão com o Banco de Dados... ");
        try (Connection connection = dataSource.getConnection()) {
            if (connection.isValid(10)) { // Timeout 10s
                System.out.println(ANSI_GREEN + "SUCESSO!" + ANSI_RESET);
                return true;
            } else {
                System.out.println(ANSI_RED + "FALHA (Conexão inválida)!" + ANSI_RESET);
                return false;
            }
        } catch (Exception e) {
            System.out.println(ANSI_RED + "FALHA!" + ANSI_RESET);
            System.out.println(ANSI_YELLOW + "   Erro: " + e.getMessage() + ANSI_RESET);
            return false;
        }
    }

    // Valida se o Controller foi corretamente injetado
    private boolean validarControllerAPI() {
        System.out.print(">> Validando inicialização da API... ");
        if (tarefaController != null) {
            System.out.println(ANSI_GREEN + "SUCESSO!" + ANSI_RESET);
            return true;
        } else {
            System.out.println(ANSI_RED + "FALHA (Controller não injetado)!" + ANSI_RESET);
            return false;
        }
    }

    // Imprime banner final com status da aplicação
    private void imprimirBanner(boolean dbStatus, boolean apiStatus) {
        String statusMessage = (dbStatus && apiStatus)
                ? ANSI_PINK + "STATUS: TUDO OK!" + ANSI_RESET
                : ANSI_RED + "STATUS: INICIALIZADO COM FALHAS!" + ANSI_RESET;

        System.out.println("\n========================================");
        System.out.println("|     API com Java Spring Boot         |");
        System.out.println("|     Por: Maria Fernanda Bronzoni     |");
        System.out.println("|     RU:  4828466                     |");
        System.out.println("|     " + statusMessage + "                 |");
        System.out.println("========================================");

        if (dbStatus && apiStatus) {
            System.out.println("\n>> API pronta para receber requisições.\n");
        } else {
            System.out.println(ANSI_RED + "\n>> A aplicação iniciou, mas um ou mais componentes críticos falharam." + ANSI_RESET);
            System.out.println(ANSI_RED + ">> Verifique os logs de erro acima.\n" + ANSI_RESET);
        }
    }
}
