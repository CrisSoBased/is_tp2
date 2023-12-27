import { Controller, Get, Post, Body, Patch, Param, Delete } from '@nestjs/common';
import { ClubsService } from './clubs.service';
import { Prisma } from '@prisma/client';

@Controller('clubs')
export class ClubsController {
  constructor(private readonly clubsService: ClubsService) {}

  @Post()
  create(@Body() createClubDto: Prisma.clubCreateInput) {
    return this.clubsService.create(createClubDto);
  }

  @Get()
  findAll() {
    return this.clubsService.findAll();
  }

  @Get(':id')
  findOne(@Param('id') id: string) {
    return this.clubsService.findOne(id as string);
  }

  @Patch(':id')
  update(@Param('id') id: string, @Body() updateClubDto: Prisma.clubUpdateInput) {
    return this.clubsService.update(id as string, updateClubDto);
  }

  @Delete(':id')
  remove(@Param('id') id: string) {
    return this.clubsService.remove(id as string);
  }
}
