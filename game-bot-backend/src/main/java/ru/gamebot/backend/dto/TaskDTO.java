package ru.gamebot.backend.dto;

import com.fasterxml.jackson.annotation.JsonFormat;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.NotNull;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
public class TaskDTO {
    private Integer id;
    @NotEmpty(groups = Create.class)
    private String name;
    @NotNull(groups = Create.class)
    private Integer money;
    @NotNull(groups = Create.class)
    private Long duration;
    @NotNull(groups = Create.class)
    private Integer chatId;
    @NotNull(groups = Create.class)
    private Integer ownerUserId;
    private Integer workerUserId;
    @NotEmpty(groups = Create.class)
    @JsonFormat(pattern="yyyy-MM-dd HH:mm:ss")
    private java.util.Date deadline;
}
