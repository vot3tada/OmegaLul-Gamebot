package ru.gamebot.backend.dto;

import com.fasterxml.jackson.annotation.JsonAlias;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;
import ru.gamebot.backend.models.PersonPK;


@Data
public class PersonDTO {
    @JsonAlias({"personPk"})
    @JsonProperty("personPk")
    private PersonDTO.PersonPKDTO personPKDTO;
    private String name;
    private Integer experience;
    private Integer experienceMultiply;
    private Integer money;
    private String photo;
    private Float luck;
    private Integer luckMultiply;
    private Integer hp;
    private Integer damage;
    private Integer damageMultiply;
    private String gitlabUserName;

    @Data
    public static class PersonPKDTO {
        private Integer chatId;
        private Integer userId;

        public PersonPKDTO() {
        }

        public PersonPKDTO(Integer chatId, Integer userId) {
            this.chatId = chatId;
            this.userId = userId;
        }
    }

    public PersonPK toPersonPK() {
        return new PersonPK(personPKDTO.chatId, personPKDTO.userId);
    }

}
