package com.bmt.MyStage.repositories;

import com.bmt.MyStage.models.AppUser;
import org.springframework.data.jpa.repository.JpaRepository;

public interface AppUserRepository extends JpaRepository<AppUser,Integer> {


    public AppUser findByEmail(String email);
}
