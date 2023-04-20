package ru.gamebot.backend.dto;

import com.fasterxml.jackson.annotation.JsonFormat;
import jakarta.validation.constraints.Future;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.NotNull;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
public class CreateEventDTO {
    private Integer id;
    @NotNull(groups = Create.class)
    private Integer chatId;
    @NotNull(groups = Create.class)
    private Integer userId;
    @NotEmpty(groups = Create.class)
    private String name;
    @Future(groups = Create.class)
    @JsonFormat(pattern="yyyy-MM-dd HH:mm:ss")
    private java.util.Date startedAt;
}