USE smart_task_tracker;

CREATE TABLE `USER` (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100) NULL,
    gmail VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE = InnoDB;

CREATE TABLE `TASK` (
    task_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(150) NOT NULL,
    description TEXT,
    importance INT NOT NULL,
    due_date DATE NULL,
    completed BOOLEAN DEFAULT FALSE,
    creator_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_task_importance CHECK (importance BETWEEN 1 AND 5),
    CONSTRAINT fk_task_creator
        FOREIGN KEY (creator_id) REFERENCES `USER`(user_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    INDEX idx_task_creator_id (creator_id)
) ENGINE = InnoDB;

CREATE TABLE `TASK_COLLABORATOR` (
    task_id INT NOT NULL,
    user_id INT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'ACCEPTED',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    accepted_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (task_id, user_id),
    CONSTRAINT fk_task_collaborator_task
        FOREIGN KEY (task_id) REFERENCES `TASK`(task_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk_task_collaborator_user
        FOREIGN KEY (user_id) REFERENCES `USER`(user_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    INDEX idx_task_collaborator_user_id (user_id)
) ENGINE = InnoDB;

CREATE TABLE `SUBTASK` (
    subtask_id INT PRIMARY KEY AUTO_INCREMENT,
    task_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_subtask_task
        FOREIGN KEY (task_id) REFERENCES `TASK`(task_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    INDEX idx_subtask_task_id (task_id)
) ENGINE = InnoDB;

