package ru.gamebot.backend.dto;

import jakarta.annotation.Nullable;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.NotNull;
import lombok.Data;
import ru.gamebot.backend.models.PersonPK;

@Data
public class PersonDTO {
    @NotNull
    private PersonDTO.PersonPKDTO personPKDTO;


    @NotEmpty(groups = CreatePerson.class)
    private String name;

    private Integer experience;


    private Integer experienceMultiply;

    private Integer money;

    @NotEmpty(groups = CreatePerson.class)
    private String photo;
    @Nullable
    private Float luck;
    @Nullable
    private Integer luckMultiply;
    @Nullable
    private Integer hp;
    @Nullable
    private Integer damage;
    @Nullable
    private Integer damageMultiply;

    @Data
    public static class PersonPKDTO {
        @NotNull(groups = CreatePerson.class)
        private int chatId;
        @NotNull(groups = CreatePerson.class)
        private int userId;

        public PersonPKDTO() {
        }

        public PersonPKDTO(int chatId, int userId) {
            this.chatId = chatId;
            this.userId = userId;
        }
    }

    public PersonPK toPersonPK() {
        return new PersonPK(personPKDTO.userId, personPKDTO.chatId);
    }

}
