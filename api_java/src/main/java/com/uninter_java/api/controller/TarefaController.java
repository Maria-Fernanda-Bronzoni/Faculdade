//-----------------------------------------------------
// Projeto: Desenvolvimento de API com Java Spring Boot
// Autora: Maria Fernanda Bronzoni
// RU: 4828466
//------------------------------------------------------

package com.uninter_java.api.controller;

import com.uninter_java.api.model.Tarefa;
import com.uninter_java.api.repository.TarefaRepository;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/tarefas")
public class TarefaController {

    private final TarefaRepository repository;

    public TarefaController(TarefaRepository repository) {
        this.repository = repository;
    }

    //Criar nova tarefa
    @PostMapping("/cadastro")
    @ResponseStatus(HttpStatus.CREATED)
    public Tarefa cadastro(@RequestBody Tarefa tarefa) { //
        return repository.save(tarefa);
    }

    // Listar todas as tarefas
    @GetMapping("/listar")
    public List<Tarefa> listar() {
        return repository.findAll();
    }

    // Buscar tarefa por ID
    @GetMapping("/buscar/{id}")
    public ResponseEntity<Tarefa> buscar(@PathVariable Long id) {
        return repository.findById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    // Atualizar tarefa
    @PutMapping("/atualizar/{id}")
    public ResponseEntity<Tarefa> atualizar(@PathVariable Long id, @RequestBody Tarefa tarefa) {
        return repository.findById(id)
                .map(registro -> {
                    registro.setNome(tarefa.getNome());
                    registro.setDataEntrega(tarefa.getDataEntrega());
                    registro.setResponsavel(tarefa.getResponsavel());
                    Tarefa tarefaAtualizada = repository.save(registro);
                    return ResponseEntity.ok(tarefaAtualizada);
                }).orElse(ResponseEntity.notFound().build());
    }

    // Deletar tarefa
    @DeleteMapping("/excluir/{id}")
    public ResponseEntity<Void> deletar(@PathVariable Long id) {
        return repository.findById(id)
                .map(registro -> {
                    repository.delete(registro);
                    return ResponseEntity.noContent().<Void>build();
                }).orElse(ResponseEntity.notFound().build());
    }
}
