import { Injectable } from '@nestjs/common';
import { Prisma } from '@prisma/client';
import { DatabaseService } from 'src/database/database.service';

@Injectable()
export class PlayersService {
  constructor(private readonly databaseService: DatabaseService){}


  async create(createPlayerDto: Prisma.playerCreateInput) {
    return this.databaseService.player.create({ data: createPlayerDto})
  }

  async findAll() {
    return this.databaseService.player.findMany({})
  }

  async findOne(id: string) {
    return this.databaseService.player.findUnique({
      where: {
        id,
      }
    })
  }

  async update(id: string, updatePlayerDto: Prisma.playerUpdateInput) {
    return this.databaseService.player.update({
      where: {
        id,
      },
      data: updatePlayerDto,
    })
  }

  async remove(id: string) {
    return this.databaseService.player.delete({
      where: {
        id,
      }
    })
  }
}
