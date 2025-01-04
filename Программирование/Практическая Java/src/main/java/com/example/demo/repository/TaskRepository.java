package com.example.demo.repository;

import com.example.demo.model.Task;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface TaskRepository extends JpaRepository<Task, Long> {
    // By extending JpaRepository, we automatically get methods like:
    // save(), findById(), findAll(), deleteById(), etc.
    
    // You can add custom query methods here if needed, for example:
    // List<Task> findByStatus(String status);
    // List<Task> findByTitleContaining(String keyword);
} 