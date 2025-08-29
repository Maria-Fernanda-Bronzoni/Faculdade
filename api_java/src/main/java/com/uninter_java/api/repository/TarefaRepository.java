//-----------------------------------------------------
// Projeto: Desenvolvimento de API com Java Spring Boot
// Autora: Maria Fernanda Bronzoni
// RU: 4828466
//------------------------------------------------------

package com.uninter_java.api.repository;

import com.uninter_java.api.model.Tarefa;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface TarefaRepository extends JpaRepository<Tarefa, Long> {
}
