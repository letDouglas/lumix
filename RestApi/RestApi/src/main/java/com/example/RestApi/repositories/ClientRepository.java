package com.example.RestApi.repositories;

import com.example.RestApi.models.Client;

import org.springframework.data.jpa.repository.JpaRepository;

public interface ClientRepository extends JpaRepository<Client, Integer> {

    public Client findByEmail(String email);

    Integer id(int id);
}
