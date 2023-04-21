package ru.gamebot.backend.models;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.OneToOne;
import lombok.Data;

@Data
@Entity
public class Boss {
    @Id
    private Integer id;
    private String name;
    private String photo;
    private Integer hp;
    private Integer damage;
    private Float luck;
    private Integer moneyReward;
    private Integer expReward;
    private Integer ultaCharge;
    private Integer cleaveRate;
    private Integer ultaRate;

    @OneToOne
    @JoinColumn(name = "item_id", referencedColumnName = "id")
    private Item item;
}
