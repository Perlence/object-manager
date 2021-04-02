# Object Manager

Object Manager exercise.

## Design

The Object Manages manages objects which are positive nonzero integers. The
object can be in one of three states:

```
+-------------+
| not managed |------------+
+-------------+     put    |
          ^                v
          |   drop    +---------+
          +-----------| in pool |------------+
                      +---------+     get    |
                              ^              v
                              |  free   +----------+
                              +---------| acquired |
                                        +----------+
```

Rules:

- **Put** adds the object to the pool, so that it can be acquired via **Get**.
- If the object *n* has been **Put** into the pool, you cannot add another object
  *n*.
- **Get** returns an arbitrary object from the pool. An object cannot be given
  away again unless it has been freed.
- Cannot **Get** an object that is not in the pool.
- **Free** returns the object back into the pool, so that it can be given out
  again.
- **Drop** removes the object from the pool.
- Cannot **Drop** an object that is currently acquired via **Get**.

## Development

1. Start the environment:

   ```sh
   docker-compose up -d env
   ```

2. Start the API server:

   ```sh
   docker-compose exec env env FLASK_APP=api.app flask run -h 0.0.0.0
   ```

4. Start the React dev server:

   ```sh
   docker-compose exec env yarn start
   ```
